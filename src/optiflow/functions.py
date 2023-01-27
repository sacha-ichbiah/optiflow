import ot
import matplotlib.pyplot as plt
import numpy as np
import polyscope as ps
import torch
import torch.nn as nn

def define_matrices(npoints,signed_dist =True,plot = False):
    C_tot = define_cost_matrix_circular(npoints)
    D_tot = define_distance_matrix_circular(npoints,signed_dist)
    
    if plot : 
        plt.figure()
        plt.imshow(C_tot,plt.cm.magma)
        plt.axis('off')
        plt.title("Cost Matrix C with circular boundary conditions")
        plt.colorbar()

        plt.figure()
        plt.imshow(D_tot,plt.cm.magma)
        plt.axis('off')
        plt.title("Dist Matrix D with circular boundary conditions")
        plt.colorbar()
        
    return(C_tot,D_tot)

def define_cost_matrix_circular(npoints):
    if npoints%2 >0 : 
        nl = (npoints+1)//2
    else : 
        nl = npoints//2
    x = np.arange(nl, dtype=np.float64)
    M = ot.dist(x.reshape((nl, 1)), x.reshape((nl, 1)))
    M_tot = np.zeros((npoints,npoints))
    M_tot[0,:nl] = M[0]
    M_tot[0,-nl+1:] = M[0][::-1][:-1]
    if npoints%2 ==0 : 
        M_tot[0,-nl]=(np.sqrt(M[0][-1])+1)**2
    for i in range(1,len(M_tot)): 
        M_tot[i] = np.roll(M_tot[i-1],1)

    return(M_tot)

def define_distance_matrix_circular(npoints,signed=True): 
    if npoints%2 >0 : 
        nl = (npoints+1)//2
    else : 
        nl = npoints//2
    x = np.arange(nl, dtype=np.float64)
    D = ot.dist(x.reshape((nl, 1)), x.reshape((nl, 1)))
    sqrtD = np.sqrt(D) 
    
    if signed : 
        sM = np.tril(sqrtD)*-1 + np.triu(sqrtD)
    else : 
        sM = sqrtD
        
    sM_tot = np.zeros((npoints,npoints))
    sM_tot[0,:nl] = sM[0]
    sM_tot[0,-nl+1:] = - sM[0][::-1][:-1]
    if npoints%2 ==0 : 
        sM_tot[0,-nl]=(sM[0][-1]+1)
    for i in range(1,len(sM_tot)): 
        sM_tot[i] = np.roll(sM_tot[i-1],1)

    return(sM_tot)
import ot

def compute_displacements_from_kymograph(K, C, D): 
    V = np.zeros(K.shape)
    for t in range(len(K[0])-1):
        try : 
            a = K[:,t].copy(order='C')
            b = K[:,t+1].copy(order='C')
            a/=np.sum(a)
            b/=np.sum(b)

            M = ot.emd(a, b, C)

            Displacements = np.zeros(len(K))
            for i in range(len(K)): 
                Displacements[i] = np.sum(D[i] * M[i]/a[i])
            V[:,t] = Displacements.copy()
        except : 
            print("ouille")
            V[:,t] = Displacements.copy()
    
    return(V[:,:-1])


def plot_vector_field(V,t,pool_size = 25):
    nlong = 1000
    points_circle_long = [[np.cos(t),np.sin(t),0] for t in np.linspace(0,2*np.pi,nlong)]
    points_circle_long = np.array(points_circle_long)
    edges = np.array([[i,i+1] for i in range(nlong)])
    edges[-1,1]=0
    ps.init()
    ps.register_curve_network("Curves",points_circle_long,edges,radius=0.002, color = (0,0,0))

    data = V[:,t]
    scale = np.amax(V)
    m = nn.AvgPool1d(pool_size, stride=pool_size)
    d = m(torch.tensor([[data]]))[0,0].numpy()
    n = len(d)
    points_circle = [[np.cos(t),np.sin(t),0] for t in np.linspace(0,2*np.pi,n)]
    points_circle = np.array(points_circle)
    ps_cloud = ps.register_point_cloud("Cloud",points_circle,radius =0)

    
    normals=np.array([0,0,1])
    vec_normal_base = np.cross(normals,points_circle)
    vec_normal = vec_normal_base.copy()
    for i in range(3) : 
        vec_normal[:,i]*=d/scale/2

    s = d.copy()
    s[15:]*=-1
    pos_vec_normal = vec_normal.copy()
    neg_vec_normal = vec_normal.copy()
    for i in range(3): 
        pos_vec_normal[:,i]*= ((s>0).astype(int))
        neg_vec_normal[:,i]*= ((s<=0).astype(int))

    ps_cloud.add_vector_quantity("Positive flows", pos_vec_normal,vectortype="ambient", enabled=True,radius = 0.013, color = [0.6745098 , 0.17254902, 0.17254902] )#, color = "#AC2C2C")
    ps_cloud.add_vector_quantity("Negative flows", neg_vec_normal,vectortype="ambient", enabled=True,radius = 0.013, color = [0.17254902, 0.28235294, 0.6745098 ] )
    ps.set_ground_plane_mode("none")
    ps.show()